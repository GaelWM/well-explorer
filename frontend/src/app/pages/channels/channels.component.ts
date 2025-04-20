import { CommonModule } from '@angular/common';
import {
  AfterViewInit,
  Component,
  ElementRef,
  inject,
  OnDestroy,
  OnInit,
  ViewChild,
} from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatTooltipModule } from '@angular/material/tooltip';
import { ActivatedRoute, RouterModule } from '@angular/router';
import * as echarts from 'echarts';
import { map, of, switchMap } from 'rxjs';
import { ConfirmDialogService } from '../../shared/components/confirm-dialog/confirm-dialog.service';
import { ChannelFormComponent } from './channel-form/channel-form.component';
import { Channel, ChannelData } from './channel.model';
import { ChannelsService } from './channels.service';

@Component({
  selector: 'app-channels',
  templateUrl: './channels.component.html',
  standalone: true,
  imports: [CommonModule, RouterModule, MatTooltipModule],
  styleUrls: ['./channels.component.css'],
})
export class ChannelsComponent implements OnInit, AfterViewInit, OnDestroy {
  readonly channelService = inject(ChannelsService);
  readonly route = inject(ActivatedRoute);
  readonly dialog = inject(MatDialog);
  readonly confirmDialogService = inject(ConfirmDialogService);

  channels: Channel[] = [];
  selectedChannel: Channel | null = null;
  channelData: ChannelData[] = [];

  // Chart related
  @ViewChild('chartContainer') chartContainer!: ElementRef;
  chart: echarts.ECharts | null = null;

  // Form related
  showChannelForm = false;
  editingChannel: Channel | null = null;

  // Delete confirmation
  channelToDelete: Channel | null = null;

  // Resize observer for chart responsiveness
  private resizeObserver: ResizeObserver | null = null;

  ngOnInit(): void {
    this.loadChannels();
  }

  ngAfterViewInit(): void {
    // Set up resize observer for chart responsiveness
    this.setupResizeObserver();
  }

  ngOnDestroy(): void {
    // Clean up chart and observer when component is destroyed
    if (this.chart) {
      this.chart.dispose();
    }

    if (this.resizeObserver) {
      this.resizeObserver.disconnect();
    }
  }

  loadChannels(): void {
    this.route.params
      .pipe(
        map((params) => params['well_id']),
        switchMap((well_id) => {
          if (!well_id) {
            console.error('Well ID is required to load channels.');
            return of([]);
          }
          return this.channelService.getChannels(well_id);
        })
      )
      .subscribe({
        next: (channels) => {
          this.channels = channels;

          // Select the first channel by default if available and none is currently selected
          if (channels.length > 0 && !this.selectedChannel) {
            this.selectChannel(channels[0]);
          }
        },
        error: (error) => {
          console.error('Error loading channels:', error);
        },
      });
  }

  selectChannel(channel: Channel): void {
    this.selectedChannel = channel;
    this.loadChannelData(channel.id);
  }

  loadChannelData(channelId: number): void {
    this.route.params
      .pipe(
        map((params) => params['well_id']),
        switchMap((well_id) => {
          if (!well_id) {
            console.error('Well ID is required to load channel data.');
            return of([]);
          }
          return this.channelService.getChannelData(well_id, channelId);
        })
      )
      .subscribe({
        next: (data) => {
          this.channelData = data;
          this.initOrUpdateChart();
        },
        error: (error) => {
          console.error(`Error loading data for channel ${channelId}:`, error);
        },
      });
  }

  initOrUpdateChart(): void {
    if (!this.selectedChannel || !this.chartContainer) {
      return;
    }

    const chartDom = this.chartContainer.nativeElement;

    // Initialize chart if it doesn't exist
    if (!this.chart) {
      this.chart = echarts.init(chartDom);
    }

    // Prepare data for ECharts
    const times = this.channelData.map((item) => {
      const date = new Date(item.time);
      return date.toLocaleTimeString(); // Format time for x-axis
    });

    const values = this.channelData.map((item) => item.value);

    // Configure and update chart
    const option: echarts.EChartsOption = {
      title: {
        text: `${this.selectedChannel.name} - Time Series Data`,
        left: 'center',
      },
      tooltip: {
        trigger: 'axis',
        formatter: (params: any) => {
          const dataIndex = params[0].dataIndex;
          const date = new Date(this.channelData[dataIndex].time);
          return `${date.toLocaleString()}<br/>${params[0].seriesName}: ${
            params[0].value
          }`;
        },
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true,
      },
      xAxis: {
        type: 'category',
        boundaryGap: false,
        data: times,
        axisLabel: {
          rotate: 30,
        },
      },
      yAxis: {
        type: 'value',
        name: 'Value',
        nameLocation: 'middle',
        nameGap: 40,
      },
      series: [
        {
          name: 'Value',
          type: 'line',
          data: values,
          smooth: true,
          symbol: 'circle',
          symbolSize: 6,
          itemStyle: {
            color: '#5470c6',
          },
          lineStyle: {
            width: 3,
          },
          areaStyle: {
            opacity: 0.3,
          },
        },
      ],
    };

    // Apply options to chart
    this.chart.setOption(option);

    // Make sure chart gets updated if container size changes
    this.chart.resize();
  }

  setupResizeObserver(): void {
    if (typeof ResizeObserver === 'undefined') {
      // Fall back for browsers without ResizeObserver support
      window.addEventListener('resize', () => {
        if (this.chart) {
          this.chart.resize();
        }
      });
      return;
    }

    this.resizeObserver = new ResizeObserver(() => {
      if (this.chart) {
        this.chart.resize();
      }
    });

    if (this.chartContainer && this.chartContainer.nativeElement) {
      this.resizeObserver.observe(this.chartContainer.nativeElement);
    }
  }

  // Channel form methods
  openChannelForm(): void {
    this.editingChannel = null;

    this.dialog
      .open(ChannelFormComponent, {
        width: '600px',
        panelClass: 'transparent',
        data: {
          channel: this.editingChannel,
          well_id: this.route.snapshot.params['well_id'],
        },
      })
      .afterClosed()
      .subscribe((result) => {
        if (result) {
        }
      });
  }

  editChannel(event: Event, channel: Channel): void {
    event.preventDefault();
    event.stopPropagation();

    this.editingChannel = channel;
    this.dialog
      .open(ChannelFormComponent, {
        width: '600px',
        panelClass: 'transparent',
        data: {
          channel: this.editingChannel,
          well_id: this.route.snapshot.params['well_id'],
        },
      })
      .afterClosed()
      .subscribe((result) => {
        if (result) {
        }
      });
  }

  saveChannel(channel: Partial<Channel>): void {
    if (this.editingChannel) {
      // Update existing channel

      this.route.params
        .pipe(
          map((params) => params['well_id']),
          switchMap((well_id) => {
            if (!well_id) {
              console.error('Well ID is required to update channel.');
              return of(null);
            }
            return this.channelService.getChannelById(
              well_id,
              this.editingChannel!.id
            );
          })
        )
        .subscribe({
          next: () => {
            this.loadChannels();
          },
          error: (error) => {
            console.error('Error updating channel:', error);
          },
        });
    } else {
      // Create new channel
      this.route.params
        .pipe(
          map((params) => params['well_id']),
          switchMap((well_id) => {
            if (!well_id) {
              console.error('Well ID is required to create channel.');
              return of(null);
            }
            return this.channelService.createChannel(well_id, channel);
          })
        )
        .subscribe({
          next: (newChannel) => {
            this.loadChannels();
            // Optionally select the new channel

            if (newChannel) {
              this.selectChannel(newChannel);
            }
          },
          error: (error) => {
            console.error('Error creating channel:', error);
          },
        });
    }
  }

  // Delete channel methods
  confirmDeleteChannel(event: Event, channel: Channel): void {
    event.preventDefault();
    event.stopPropagation();

    this.confirmDialogService
      .openConfirmDialog({
        title: 'Delete Confirmation',
        message:
          'Are you sure you want to delete this channel? This action cannot be undone.',
      })
      .subscribe((result) => {
        if (result) {
          this.channelService
            .deleteChannel(channel.well_id, channel.id)
            .subscribe({
              next: (success) => {},
              error: (error) => {
                console.error('Error deleting well:', error);
              },
            });
        }
      });
  }

  generateChannelData(event: Event, channel: Channel): void {
    event.preventDefault();
    event.stopPropagation();

    this.confirmDialogService
      .openConfirmDialog({
        title: 'Data Generation Confirmation',
        message:
          'Are you sure you want to generate data for this channel? This action will overwrite existing data.',
      })
      .subscribe((result) => {
        if (result) {
          this.route.params
            .pipe(
              map((params) => params['well_id']),
              switchMap((well_id) => {
                if (!well_id) {
                  console.error(
                    'Well ID is required to generate channel data.'
                  );
                  return of(null);
                }
                return this.channelService.generateChannelData(
                  well_id,
                  channel.id,
                  channel
                );
              })
            )
            .subscribe({
              next: (channelData) => {
                if (channelData) {
                  this.loadChannelData(channelData.id);
                }
              },
              error: (error) => {
                console.error('Error generating channel data:', error);
              },
            });
        }
      });
  }

  deleteChannel(): void {
    if (this.channelToDelete) {
      this.route.params
        .pipe(
          map((params) => params['well_id']),
          switchMap((well_id) => {
            if (!well_id) {
              console.error('Well ID is required to delete channel.');
              return of(null);
            }
            return this.channelService.getChannelById(
              well_id,
              this.channelToDelete!.id
            );
          })
        )
        .subscribe({
          next: (success) => {
            if (success) {
              // Check if the deleted channel was selected
              if (this.selectedChannel?.id === this.channelToDelete?.id) {
                this.selectedChannel = null;
                if (this.chart) {
                  this.chart.clear();
                }
              }

              // Reload channels
              this.loadChannels();
            }
            this.channelToDelete = null;
          },
          error: (error) => {
            console.error('Error deleting channel:', error);
            this.channelToDelete = null;
          },
        });
    }
  }
}
