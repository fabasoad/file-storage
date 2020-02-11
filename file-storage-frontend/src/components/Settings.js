export default class Settings {

    schema() {
        return 'http';
    }

    host() {
        return 'localhost';
    }

    port() {
        return process.env.FILESTORAGE_BACKEND_PORT || 8080;
    }
}