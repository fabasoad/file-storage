import React from 'react';

export default class UploadFile extends React.Component {
    state = {
        error: undefined
    };
    handleUploadFile = (e) => {
        e.preventDefault();
        const file = e.target.elements.file.value.trim();
        const error = this.props.handleUploadFile(file);

        this.setState(() => ({ error }));

        if (!error) {
            e.target.elements.file.value = '';
        }   
    };
    render() {
        return (
            <div>
                {this.state.error && <p className="upload-file-error">{this.state.error}</p>}
                <form className="upload-file" onSubmit={this.handleUploadFile}>
                    <input className="upload-file__input" type="file" name="file" />
                    <button type="submit" className="button">Upload</button>
                </form>
            </div>
        );
    }
}