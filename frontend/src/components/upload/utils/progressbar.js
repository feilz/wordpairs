import React from 'react';
import './progressbar.css';

const ProgressBar = props => {
    return (
        <div className="ProgressBar">
            <div className="Progress" style={{width: props.progress + '%'}} />
        </div>
    );
};

export default ProgressBar;
