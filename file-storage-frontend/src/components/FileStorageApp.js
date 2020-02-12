import React from 'react';
import UploadFile from './UploadFile';
import Header from './Header';
import Files from './Files';
import Settings from './Settings';

export default class FileStorageApp extends React.Component {
    state = {
        files: []
    };
    buildUrl = (fileName = '') => {
        const settings = new Settings();
        return `${settings.schema()}://${settings.host()}:${settings.port()}/files` + (!!fileName ? `/${fileName}` : '');
    };
    handleDeleteFiles = () => {
        this.setState(() => ({ files: [] }));
    };
    handleDeleteFile = (file) => {
        this.setState((prevState) => ({
            files: prevState.files.filter(x => x !== file)
        }));
    };
    handleUploadFile = (file) => {
        if (!!file) {
            const fileName = file.replace(/^.*[\\\/]/, '');
            if (this.state.files.indexOf(fileName) > -1) {
                return 'This file already exists';
            }
            this.setState((prevState) => ({
                files: prevState.files.concat([fileName])
            }));
        } else {
            return 'Please choose file by pressing "Choose File" button';
        }
    };
    componentDidMount() {
        fetch(this.buildUrl())
            .then(res => res.json())
            .then((data) => {
                this.setState(() => ({ skip: true, files: data.map(f => f.filename) }));
            });
    }
    componentDidUpdate(prevProps, prevState) {
        if (this.state.skip) {
            this.setState(() => ({ skip: false, files: this.state.files }));
            return;
        }
        if (prevState.files.length > this.state.files.length) {
            const result = [];
            prevState.files.filter((f) => !this.state.files.includes(f)).forEach(fileName => {
                fetch(this.buildUrl(fileName), { method: "DELETE" })
                    .then(res => res.json())
                    .then((f) => result.push([f.filename, true]))
                    .catch(() => result.push([f.filename, false]));
            });
            if (result.some(a => !a[1])) {
                this.setState(() => ({ files: result.filter(a => a[1]).map(a => a[0]) }));
            }
        } else if (prevState.files.length < this.state.files.length) {
            const result = [];
            this.state.files.filter((f) => !prevState.files.includes(f)).forEach(fileName => {
                const formData = new FormData();
                formData.append('file', fileName);
                fetch(this.buildUrl(fileName), { method: "POST", body: formData })
                    .then(res => res.json())
                    .then((f) => result.push([f.filename, true]))
                    .catch(() => result.push([f.filename, false]));
            });
            if (result.some(a => !a[1])) {
                this.setState(() => ({ files: result.filter(a => a[1]).map(a => a[0]) }));
            }
        }
    }
    render() {
        const subtitle = "All your files in one place";

        return (
            <div id="app">
                <Header subtitle={subtitle} />
                <div className="container">
                    <div className="widget">
                        <Files
                            files={this.state.files}
                            handleDeleteFiles={this.handleDeleteFiles}
                            handleDeleteFile={this.handleDeleteFile}
                        />
                        <UploadFile handleUploadFile={this.handleUploadFile} />
                    </div>
                </div>
            </div>
        );
    }
}