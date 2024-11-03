from pydantic import BaseModel, Field

class DatabaseConnectionSchema(BaseModel):
    system_id: str = Field(..., description="Unique identifier for the system")
    username: str = Field(..., description="Username for the database connection")
    password: str = Field(..., description="Password for the database connection", min_length=8)
    ip_address: str = Field(..., description="IP address of the database server")
    port: int = Field(..., description="Port number for the database server", ge=1, le=65535)
    service_name: str = Field(..., description="Service name of the database")

    class Config:
        schema_extra = {
            "example": {
                "system_id": "sys_001",
                "username": "admin",
                "password": "your_password",
                "ip_address": "192.168.1.1",
                "port": 1521,
                "service_name": "ORCL"
            }
        }