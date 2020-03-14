import React, {useState} from 'react';
import {BrowserRouter as Router, Switch, Route} from 'react-router-dom';
import DataProvider from './components/DataProvider';
import Table from './components/Table';
import Upload from './components/upload/Upload';
import Navbar from './components/Navbar';

export default () => {
    const [topTableData, setTopTableData] = useState([]);
    const [order, setOrder] = useState({});

    const callFunc = async () => {
        const res = await fetch('http://localhost:8000/api/scan/');
        console.log(res);
    };

    const sortFunc = sortKey => {
        const data = topTableData;
        const sortOrder = order[sortKey] ? !order[sortKey] : true;
        const newData = data.sort((obj1, obj2) =>
            sortOrder
                ? obj1[sortKey] > obj2[sortKey]
                    ? -1
                    : obj1[sortKey] < obj2[sortKey]
                    ? 1
                    : 0
                : obj1[sortKey] < obj2[sortKey]
                ? -1
                : obj1[sortKey] > obj2[sortKey]
                ? 1
                : 0
        );
        setOrder({...order, [sortKey]: sortOrder});
        setTopTableData([...newData]);
    };

    const getData = async url => {
        const response = await fetch(url, {mode: 'cors'});
        console.log(response);
        if (response.status !== 200) {
            console.log('something went wrong');
            return;
        }
        const data = response.json();
        data.then(data => {
            if (!Array.isArray(data)) data = [data];
            setTopTableData(data);
        });
    };

    return (
        <div className="container">
            <Router>
                <Navbar />
                <div className="block">
                    <button
                        type="submit"
                        onClick={() =>
                            getData('http://localhost:8000/api/word/')
                        }>
                        Word
                    </button>
                    <button
                        type="submit"
                        onClick={() =>
                            getData('http://localhost:8000/api/wordrelation/')
                        }>
                        WordRelation
                    </button>
                    <Switch>
                        <Route path="/upload/">
                            <Upload endpoint="http://localhost:8000/api/fileupload/" />
                        </Route>
                        <Route path="/">
                            <Table
                                data={topTableData}
                                mSort={v => sortFunc(v)}
                                getNewData={url => getData(url)}
                            />
                        </Route>
                    </Switch>
                    <button type="submit" onClick={() => callFunc}>
                        TestScan
                    </button>
                </div>
            </Router>
        </div>
    );
};
