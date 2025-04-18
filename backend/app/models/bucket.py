from sqlalchemy import Column, Integer, Float, DateTime, inspect # type: ignore


from app.core.database import Base, engine

# Store created bucket models to avoid recreation
_bucket_models = {}

def get_bucket_model(well_name, channel_name):
    """
    Dynamically create or retrieve a bucket model for a specific well and channel
    
    Args:
        well_name (str): Name of the well
        channel_name (str): Name of the channel
        
    Returns:
        SQLAlchemy model class for the bucket
    """
    # Create a valid table name from well_name and channel_name
    # Replace invalid chars with underscores and lowercase everything
    def sanitize_name(name):
        return ''.join(c.lower() if c.isalnum() else '_' for c in name)
    
    well_name_safe = sanitize_name(well_name)
    channel_name_safe = sanitize_name(channel_name)
    
    table_name = f"bucket_{well_name_safe}_{channel_name_safe}"
    
    # Return existing model if already created
    if table_name in _bucket_models:
        return _bucket_models[table_name]
    
    # Create a new model
    class Bucket(Base):
        __tablename__ = table_name
        
        id = Column(Integer, primary_key=True, index=True)
        time = Column(DateTime, nullable=False, index=True)
        value = Column(Float, nullable=False)
        
        def __repr__(self):
            return f"<Bucket {table_name} at {self.time}: {self.value}>"
    
    # Store the model for future use
    _bucket_models[table_name] = Bucket
    
    # Create the table if it doesn't exist
    if not engine.dialect.has_table(engine, table_name):
        Base.metadata.create_all(engine, tables=[Bucket.__table__])
    
    return Bucket

def get_all_bucket_tables():
    """
    Get a list of all bucket tables in the database
    
    Returns:
        List of table names that start with 'bucket_'
    """
    inspector = inspect(engine)
    all_tables = inspector.get_table_names()
    return [table for table in all_tables if table.startswith('bucket_')]

def get_bucket_model_by_names(well_name, channel_name):
    """
    Get the bucket model for a specific well and channel,
    but don't create it if it doesn't exist
    
    Args:
        well_name (str): Name of the well
        channel_name (str): Name of the channel
        
    Returns:
        SQLAlchemy model class for the bucket or None if it doesn't exist
    """
    def sanitize_name(name):
        return ''.join(c.lower() if c.isalnum() else '_' for c in name)
    
    well_name_safe = sanitize_name(well_name)
    channel_name_safe = sanitize_name(channel_name)
    
    table_name = f"bucket_{well_name_safe}_{channel_name_safe}"
    
    # Return existing model if already created
    if table_name in _bucket_models:
        return _bucket_models[table_name]
    
    # Check if table exists in database
    if not engine.dialect.has_table(engine, table_name):
        return None
    
    # Create and return the model
    return get_bucket_model(well_name, channel_name)