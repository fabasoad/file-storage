import React from 'react';
import AddOption from './AddOption';
import Header from './Header';
import Files from './Files';
import Settings from './Settings';

export default class FileStorageApp extends React.Component {
    state = {
        files: []
    };
    handleDeleteFiles = () => {
        this.setState(() => ({ files: [] }));
    };
    handleDeleteFile = (option) => {
        this.setState((prevState) => ({
            files: prevState.files.filter(x => x !== option)
        }));
    };
    handleAddFile = (option) => {
        if (!option) {
            return 'Enter valid value to add item';
        } else if (this.state.files.indexOf(option) > -1) {
            return 'This file already exists';
        }
        this.setState((prevState) => ({
            files: prevState.files.concat([option])
        }));
    };
    componentDidMount() {
        const settings = new Settings();
        fetch(`${settings.schema()}://${settings.host()}:${settings.port()}/files`)
        .then(res => res.json())
        .then((data) => {
            this.setState(() => ({ files: data.map(f => f.filename) }));
        })
        .catch(console.log)
    }
    componentDidUpdate(prevProps, prevState) {
        if (prevState.files.length !== this.state.files.length) {
            const json = JSON.stringify(this.state.files);
            localStorage.setItem('files', json);
        }
    }
    componentWillUnmount() {
        console.log('componentWillUnmount');
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
                        <AddOption handleAddFile={this.handleAddFile} />
                    </div>
                </div>
            </div>
        );
    }
}