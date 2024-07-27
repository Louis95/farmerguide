# Farmer's Guide

```mermaid
erDiagram
    USER {
        int id PK
        string username
        string email
        string hashed_password
        datetime created_at
        datetime updated_at
    }
    FARM {
        int id PK
        string name
        string location
        float size
        datetime created_at
        datetime updated_at
    }
    SOIL_HEALTH {
        int id PK
        int farm_id
        float ph_level
        float nitrogen_level
        float phosphorus_level
        float potassium_level
        float organic_matter
        datetime analysis_date
        text recommendations
    }
    NOTIFICATION {
        int id PK
        int user_id
        text message
        string notification_type
        boolean is_read
        datetime created_at
    }
    FARMING_ADVICE {
        int id PK
        int farm_id
        string advice_type
        text content
        datetime created_at
    }
    CROP_DISEASE {
        int id PK
        int farm_id
        string crop_type
        string disease_name
        float confidence
        string image_url
        text treatment_recommendation
        datetime detected_at
    }
    USER_FARM {
        int user_id PK
        int farm_id PK
        string role
        datetime created_at
        datetime updated_at
    }

    USER ||--o{ USER_FARM : has
    FARM ||--o{ USER_FARM : has
    USER ||--o{ NOTIFICATION : receives
    FARM ||--o{ SOIL_HEALTH : has
    FARM ||--o{ FARMING_ADVICE : receives
    FARM ||--o{ CROP_DISEASE : has
    FARM ||--o{ USER_FARM : has many
    SOIL_HEALTH }o--|| FARM : belongs to
    NOTIFICATION }o--|| USER : belongs to
    FARMING_ADVICE }o--|| FARM : belongs to
    CROP_DISEASE }o--|| FARM : belongs to
    USER_FARM }o--|| USER : belongs to
    USER_FARM }o--|| FARM : belongs to

```

### Explanation
- **Entities**:
  - `USER`, `FARM`, `SOIL_HEALTH`, `NOTIFICATION`, `FARMING_ADVICE`, `CROP_DISEASE`, `USER_FARM`
  
- **Relationships**:
  - Users can have many notifications, and notifications belong to one user.
  - Farms can have many soil health records, farming advice, crop diseases, and user-farm relationships.
  - Soil health records, farming advice, and crop diseases belong to one farm.
  - The `USER_FARM` table creates a many-to-many relationship between users and farms, with additional attributes such as role, created_at, and updated_at.