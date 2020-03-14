import React from 'react';
import {Link} from 'react-router-dom';

export default () => (
    <div className="block">
        <nav className="navbar">
            <div className="navbar-brand">
                <Link to="/" className="navbar-item">
                    <h1 className="title is-4">Word relation analyzer</h1>
                </Link>
                <div className="navbar-burger"></div>
            </div>
            <div className="navbar-menu is-active">
                <div className="navbar-start"></div>
                <div className="navbar-end">
                    <Link to="/" className="navbar-item">
                        Home
                    </Link>
                    <Link to="/upload" className="navbar-item">
                        Upload
                    </Link>
                </div>
            </div>
        </nav>
    </div>
);
