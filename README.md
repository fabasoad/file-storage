# File storage app
## REST application
### Run application manually
#### Prerequisites
1. Python - 3.7.6
2. Pip - 20.0.2
3. Redis - 5.0.7
4. Yarn - 1.16.0
#### Steps
##### Build frontend
1. Install yarn.
2. Change path to file-storage-backend folder based on your local env in `webpack.common.js` (line 37).
2. Run the following commands:
```bash
yarn install
yarn run build:prod
```
##### Build backend
1. Install and run Redis instance with password.
2. Define environment variables:
    1. FILESTORAGE_BACKEND_HOST - (Optional) Host where your application will be up and running. Default - `0.0.0.0`.
    2. FILESTORAGE_BACKEND_PORT - (Optional) Port where your application will be up and running. Default - `8080`.
    3. FILESTORAGE_PATH - (Optional) Path where files will be stored. Default - `/usr/files`.
    4. REDIS_HOST - (Optional) Host where Redis instance is running. Default: `0.0.0.0`.
    5. REDIS_PORT - (Optional) Port where Redis instance is running. Default: `6379`.
    6. REDIS_PASSWORD - (Required) Password for access to Redis instance.
3. Install Dependencies
```bash
pip install -r requirements.txt
```
4. Run Application
```bash
python -m src.rest
```
### Run application using Docker
#### Prerequisites
1. Docker - 19.03.5
2. Docker-Compose - 1.24.1
#### Steps
1. Create `./docker/.env` file with the following content:
```bash
VERSION=1.0.0
PORT=8080
FILESTORAGE_PATH=/usr/local/temp
```
2. Run `docker-compose` command:
```bash
cd ./docker
docker-compose -f "docker-compose.yml" up -d --build
```
### Debug Application
#### VS Code
1. Create `.vscode/launch.json` file with the following content:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: File Storage",
            "type": "python",
            "request": "launch",
            "module": "src.rest"
        }
    ]
}
```
2. Go to the Debug tab and run your configuration.
## CLI application
### Run application manually
#### Prerequisites
1. Python - 3.7.6
2. Pip - 20.0.2
#### Steps
1. Run REST application following by previous section
2. Define environment variables:
    1. FILESTORAGE_SCHEMA - (Optional) Protocol where REST application is up and running. Default - `http`.
    2. FILESTORAGE_HOST - (Optional) Host where REST application is up and running. Default - `127.0.0.1`.
    3. FILESTORAGE_PORT - (Optional) Port where REST application is up and running. Default - `8080`.
3. Run CLI help function to see possible options:
```bash
pip install -r requirements.txt
python -m src.cli --help
```