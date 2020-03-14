import React, {useState} from 'react';
import './Dropzone.css';

const Dropzone = props => {
    const textInput = React.createRef();
    const [highlight, setHighlight] = useState(false);

    const onFilesAdded = e => {
        if (props.disabled) return;
        if (props.onFilesAdded) props.onFilesAdded([...e.target.files]);
    };
    const openFileDialog = () => {
        if (props.disabled) return;
        textInput.current.click();
    };

    const onDragOver = e => {
        e.preventDefault();
        if (props.disabled) return;
        setHighlight(true);
    };

    const onDrop = e => {
        if (props.disabled) return;
        const files = e.dataTransfer.files;
        if (props.onFilesAdded) {
            const array = [...files];
            props.onFilesAdded(array);
        }
        setHighlight(true);
    };

    return (
        <div
            className={`Dropzone ${highlight ? 'Highlight' : ''}`}
            onClick={openFileDialog}
            onDragOver={onDragOver}
            onDragLeave={() => setHighlight(false)}
            onDrop={onDrop}
            style={{cursor: props.disabled ? 'default' : 'pointer'}}>
            <img alt="upload" className="Icon" src="cloud_upload-24px.svg" />
            <input
                ref={textInput}
                className="FileInput"
                type="file"
                multiple
                onChange={onFilesAdded}
            />
            <span>Upload Files</span>
        </div>
    );
};

export default Dropzone;
