// wells-map.component.ts
import { CommonModule } from '@angular/common';
import { AfterViewInit, Component, Input, OnInit } from '@angular/core';
import * as L from 'leaflet';
import { LiftType, Well, WellStatus } from '../../wells/well.model';

@Component({
  selector: 'app-map',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.css'],
})
export class MapComponent implements OnInit, AfterViewInit {
  @Input() set wells(value: Well[]) {
    this._wells = value;
    if (this.map) {
      this.loadWellsOnMap();
      this.fitMapToWells();
    }
  }
  get wells(): Well[] {
    return this._wells;
  }
  private _wells: Well[] = [];

  private map!: L.Map;
  private wellMarkers: L.Marker[] = [];

  // Define icon paths for different well types and statuses
  private readonly iconPaths = {
    [LiftType.NF]: {
      [WellStatus.ACTIVE]: 'icons/nf-active.svg',
      [WellStatus.INACTIVE]: 'icons/nf-inactive.svg',
      [WellStatus.ABANDONED]: 'icons/nf-abandoned.svg',
    },
    [LiftType.GL]: {
      [WellStatus.ACTIVE]: 'icons/gl-active.svg',
      [WellStatus.INACTIVE]: 'icons/gl-inactive.svg',
      [WellStatus.ABANDONED]: 'icons/gl-abandoned.svg',
    },
    [LiftType.ESP]: {
      [WellStatus.ACTIVE]: 'icons/esp-active.svg',
      [WellStatus.INACTIVE]: 'icons/esp-inactive.svg',
      [WellStatus.ABANDONED]: 'icons/esp-abandoned.svg',
    },
  };

  // Define fallback icon colors based on status
  private readonly statusColors = {
    [WellStatus.ACTIVE]: '#22c55e', // green-500
    [WellStatus.INACTIVE]: '#f59e0b', // amber-500
    [WellStatus.ABANDONED]: '#ef4444', // red-500
  };

  constructor() {}

  ngOnInit(): void {}

  ngAfterViewInit(): void {
    this.initMap();
    this.loadWellsOnMap();
  }

  private initMap(): void {
    // Set up the Leaflet map
    this.map = L.map('wells-map', {
      center: [0, 0], // Default center (will be adjusted based on wells)
      zoom: 5,
      layers: [
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
          maxZoom: 19,
          attribution: '© OpenStreetMap contributors',
        }),
      ],
    });

    console.log('this.wells: ', this.wells);

    // If no wells, center on a default location
    if (this.wells.length === 0) {
      this.map.setView([0, 0], 2);
      return;
    }

    // Otherwise, fit the map to contain all wells
    this.fitMapToWells();
  }

  private fitMapToWells(): void {
    if (this.wells.length === 0) return;

    const latLngs = this.wells.map((well) =>
      L.latLng(well.latitude, well.longitude)
    );

    const bounds = L.latLngBounds(latLngs);
    this.map.fitBounds(bounds, { padding: [50, 50] });
  }

  private loadWellsOnMap(): void {
    // Clear existing markers
    this.clearMarkers();

    // Add wells to the map
    this.wells.forEach((well) => {
      const marker = this.createWellMarker(well);
      marker.addTo(this.map);
      this.wellMarkers.push(marker);
    });
  }

  private createWellMarker(well: Well): L.Marker {
    // Create custom icon for the well based on its type and status
    const icon = this.createWellIcon(well);

    // Create marker with custom icon
    const marker = L.marker([well.latitude, well.longitude], { icon });

    // Add a popup with well information
    marker.bindPopup(this.createWellPopup(well));

    return marker;
  }

  private createWellIcon(well: Well): L.Icon | L.DivIcon {
    // Create a Leaflet icon with the appropriate image or fallback
    try {
      return L.icon({
        iconUrl: this.iconPaths[well.lift_type][well.status],
        iconSize: [32, 32],
        iconAnchor: [16, 32],
        popupAnchor: [0, -32],
      });
    } catch (error) {
      // Fallback to colored circle marker if image not available
      console.warn(
        `Icon not found for well type ${well.lift_type} with status ${well.status}`
      );
      return L.divIcon({
        className: 'custom-div-icon',
        html: `<div style="background-color: ${
          this.statusColors[well.status]
        };" class="marker-pin">
                <span class="marker-text">${well.lift_type.charAt(0)}</span>
              </div>`,
        iconSize: [30, 30],
        iconAnchor: [15, 30],
        popupAnchor: [0, -30],
      });
    }
  }

  private createWellPopup(well: Well): string {
    // Format installation date if available
    const installation_date = well.installation_date
      ? new Date(well.installation_date).toLocaleDateString()
      : 'Not specified';

    // Create HTML content for the popup
    return `
      <div style="width: 500px" class="well-popup">
        <h3 class="font-bold text-lg">${well.name}</h3>
        <div class="grid grid-cols-2 gap-1 mt-2">
          <span class="font-semibold">ID:</span>
          <span>${well.id}</span>
          
          <span class="font-semibold">Lift Type:</span>
          <span>${well.lift_type}</span>
          
          <span class="font-semibold">Region:</span>
          <span>${well.region}</span>
          
          <span class="font-semibold">Status:</span>
          <span>${well.status}</span>
          
          <span class="font-semibold">Depth:</span>
          <span>${well.depth} meters</span>
          
          <span class="font-semibold">Installed:</span>
          <span>${installation_date}</span>
          
          <span class="font-semibold">Coordinates:</span>
          <span>${well.latitude.toFixed(6)}, ${well.longitude.toFixed(6)}</span>
        </div>
      </div>
    `;
  }

  private clearMarkers(): void {
    this.wellMarkers.forEach((marker) => {
      marker.removeFrom(this.map);
    });
    this.wellMarkers = [];
  }

  // Public methods for external components to interact with the map
  public refreshMap(): void {
    // Can be called when wells data changes
    this.loadWellsOnMap();
    this.fitMapToWells();
  }

  public filterWellsByStatus(status: WellStatus | null): void {
    this.clearMarkers();

    const filteredWells = status
      ? this.wells.filter((well) => well.status === status)
      : this.wells;

    filteredWells.forEach((well) => {
      const marker = this.createWellMarker(well);
      marker.addTo(this.map);
      this.wellMarkers.push(marker);
    });

    this.fitMapToWells();
  }

  public filterWellsByLift_type(lift_type: LiftType | null): void {
    this.clearMarkers();

    const filteredWells = lift_type
      ? this.wells.filter((well) => well.lift_type === lift_type)
      : this.wells;

    filteredWells.forEach((well) => {
      const marker = this.createWellMarker(well);
      marker.addTo(this.map);
      this.wellMarkers.push(marker);
    });

    this.fitMapToWells();
  }
}
