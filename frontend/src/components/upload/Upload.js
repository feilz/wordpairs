import React, {useState} from 'react';
import axios from 'axios';
import Dropzone from './utils/Dropzone';
import ProgressBar from './utils/progressbar';
import './Upload.css';

const Upload = props => {
    const [uploading, setUploading] = useState(false);
    const [uploadProgress, setUploadProgress] = useState({});
    const [successfulUploaded, setSuccessfulUploaded] = useState(false);
    const [files, setFiles] = useState([]);

    const onFilesAdded = newFiles => setFiles([...files, ...newFiles]);

    const renderProgress = file => {
        const thisProgress = uploadProgress[file.name];
        return uploading || successfulUploaded ? (
            <div className="ProgressWrapper">
                <ProgressBar
                    progress={thisProgress ? thisProgress.percentage : 0}
                />
                <img
                    className="CheckIcon"
                    alt="done"
                    src="check_circle_outline-24px.svg"
                    style={{
                        opacity:
                            thisProgress && thisProgress.state === 'done'
                                ? 0.5
                                : 0
                    }}
                />
            </div>
        ) : (
            <div />
        );
    };

    const renderActions = () => {
        return successfulUploaded ? (
            <button
                onClick={() => {
                    setFiles([]);
                    setSuccessfulUploaded(false);
                }}>
                Clear
            </button>
        ) : (
            <button
                disabled={files.length < 0 || uploading}
                onClick={uploadFiles}>
                Upload
            </button>
        );
    };

    const sendRequest = file => {
        const fd = new FormData();
        fd.append('file', file);
        const progressEventListener = event => {
            const progressCopy = {...uploadProgress};
            progressCopy[file.name] = {
                state: event.type,
                percentage: (event.loaded / event.total) * 100
            };
        };
        const config = {
            onUploadProgress: progressEvent =>
                progressEventListener(progressEvent)
        };
        axios.post(props.endpoint, fd, config);
    };

    const uploadFiles = async () => {
        setUploadProgress({});
        setUploading(true);
        const promises = [];
        files.forEach(file => [...promises, sendRequest(file)]);
        try {
            await Promise.all(promises);
            setSuccessfulUploaded(true);
            setUploading(false);
        } catch (e) {
            //skipping production ready for now...
            setSuccessfulUploaded(true);
            setUploading(false);
            console.log('upload failed miserably...');
        }
    };

    return (
        <div className="Upload">
            <span className="Title">Upload Files</span>
            <div className="Content">
                <Dropzone
                    onFilesAdded={onFilesAdded}
                    disabled={uploading || successfulUploaded}
                />
                <div className="Files">
                    {files.map(file => (
                        <div key={file.name} className="Row">
                            <span className="FileName">{file.name}</span>
                            {renderProgress(file)}
                        </div>
                    ))}
                </div>
            </div>
            <div className="Actions">{renderActions()}</div>
        </div>
    );
};

export default Upload;
