import React from 'react';
import File from './File';

const Files = (props) => (
    <div>
        <div className="widget-header">
            <h3 className="widget-header__title">Your files</h3>
            <button
                className="button button--link"
                onClick={props.handleDeleteFiles}
            >
                Remove all
            </button>            
        </div>
        {props.files.length === 0 && <p className="widget__message">Please upload a file to get started</p>}
        {
            props.files.map((file, index) =>
                <File
                    key={file}
                    fileName={file}
                    count={index + 1}
                    handleDeleteFile={props.handleDeleteFile}
                />)
        }
    </div>
);

export default Files;