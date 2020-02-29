# File storage app
## Run REST application
### Prerequisites
1. Docker - 19.03.5
2. Docker-Compose - 1.24.1
### Steps
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
> It will take a while to up and run application (around 7-10 minutes).
3. Open `http://127.0.0.1:8080/` in browser.
## Run CLI application
### Prerequisites
1. Python - 3.7.6
2. Pip - 20.0.2
### Steps
1. Run REST application following by previous section
2. Define environment variables:
    1. FILESTORAGE_SCHEMA - (Optional) Protocol where REST application is up and running. Default - `http`.
    2. FILESTORAGE_HOST - (Optional) Host where REST application is up and running. Default - `127.0.0.1`.
    3. FILESTORAGE_PORT - (Optional) Port where REST application is up and running. Default - `8080`.
3. Run CLI help function to see possible options:
```bash
cd ./file-storage-backend
pip install -r requirements.txt
python -m src.cli --help
```
## Debug Application
### VS Code
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
## Run REST application manually
> In case something went wrong with Docker running
1. Extract content from `dist.zip` to `file-storage-backend/public/` folder.
2. Install Python 3 and Pip.
3. Install and run Redis with password.
4. Run the following command (Linux):
```bash
export FILESTORAGE_PATH=<Path to files folder>
export FILESTORAGE_BACKEND_HOST=127.0.0.1
export FILESTORAGE_BACKEND_PORT=8080
export REDIS_HOST=127.0.0.1
export REDIS_PORT=6379
export REDIS_PASSWORD=<PASSWORD>
cd ./file-storage-backend
pip install -r requirements.txt
python -m src.rest
```
4. Open `http://127.0.0.1:8080/` in browser.
## Run Tests
### Backend
#### REST Tests
1. Run server with clean state
2. Run the command below.
```bash
# export commands are optional
export REST_SCHEMA='http' # default is 'http'
export REST_HOST='localhost' # default is '127.0.0.1'
export REST_PORT=8080 # default is 8080
cd ./file-storage-backend
pip install -r requirements.txt
pytest ./src/rest_tests
```
#### Unit Tests
1. Run the commands below.
```bash
cd ./file-storage-backend
pip install -r requirements.txt
pytest ./src/service
```
### Frontend
#### Unit tests
1. Install `yarn`.
2. Run the commands below.
```bash
cd ./file-storage-frontend
yarn install
yarn run test
```