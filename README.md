# Cafe Management System

## Endpoints

### 1. Get Random Cafe

- **URL**: `/random`
- **Method**: `GET`
- **Description**: Retrieves a random cafe from the database.

### 2. Get All Cafes

- **URL**: `/all`
- **Method**: `GET`
- **Description**: Lists all cafes in the database.

### 3. Find Cafe by Location

- **URL**: `/select`
- **Method**: `GET`
- **Query Parameter**: `location` (e.g., `?location=Kathmandu`)
- **Description**: Finds cafes by location.

### 4. Add New Cafe

- **URL**: `/add`
- **Method**: `POST`
- **Form Data**:
  - `name`
  - `map_url`
  - `img_url`
  - `location`
  - `seats`
  - `has_toilet` (true/false)
  - `has_wifi` (true/false)
  - `has_sockets` (true/false)
  - `can_take_calls` (true/false)
  - `coffee_price`

- **Description**: Adds a new cafe to the database.

### 5. Update Cafe Price

- **URL**: `/update_price/<int:cafe_id>`
- **Method**: `PATCH`
- **Query Parameter**: `new_price`
- **Description**: Updates the coffee price for a specified cafe.

### 6. Delete Cafe

- **URL**: `/report_closed/<int:cafe_id>`
- **Method**: `DELETE`
- **Query Parameter**: `api_key`
- **Description**: Deletes a cafe from the database. Requires `api_key` for authentication.
