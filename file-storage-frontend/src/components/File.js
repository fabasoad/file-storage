import React from 'react';

const File = (props) => (
    <div className="option">
        <p className="option__text">{props.count}. {props.fileName}</p>
        <button
            className="button button--link"
            onClick={(e) => {
                props.handleDeleteFile(props.fileName);
            }}
        >
            Remove
        </button>
    </div>
);

export default File;