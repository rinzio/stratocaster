### Installation

1. [Install Docker](https://www.docker.com)
2. Run `docker compose up --build`
3. Go to `http://127.0.0.1:8000/docs`

### Notes

1. Add a file named `dev.env` to project's root.
2. Add this content to it:
    ```
    MONGO_URI="mongodb://db:27017/"
    MONGO_DB="poc"
    ```
