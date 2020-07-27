import React, {useState} from 'react';
import {BrowserRouter as Router, Switch, Route} from 'react-router-dom';
import DataProvider from './components/DataProvider';
import Table from './components/Table';
import Upload from './components/upload/Upload';
import Navbar from './components/Navbar';

export default () => {
    const [topTableData, setTopTableData] = useState([]);
    const [supportData, setSupportData] = useState([]);
    const [paginationUrls, setPaginationUrls] = useState({});
    const [supportPaginationUrls, setSupportPaginationUrls] = useState({});

    const callFunc = async () => {
        console.log("rescan test");
        const res = await fetch('http://localhost:8000/api/scan/');
        console.log(res);
    };

    const getRelatedData = async (url, wrd) => {
        const response = await fetch(url, {mode: 'cors'});
        if (response.status !== 200) {
            console.log('something went wrong');
            return;
        }
        const data = response.json();
        data.then(data => {
            //if (!Array.isArray(data)) data = [data];
            console.log(data);
            setSupportData(data.results);
            setTopTableData(topTableData.filter(data => data.word === wrd));
            setSupportPaginationUrls({next: data.next, prev: data.previous});
        });
    };

    const getData = async url => {
        const response = await fetch(url, {mode: 'cors'});
        //console.log(response);
        if (response.status !== 200) {
            console.log('something went wrong');
            return;
        }
        const data = response.json();
        data.then(data => {
            //if (!Array.isArray(data)) data = [data];
            console.log(data);
            setTopTableData(data.results);
            setPaginationUrls({next: data.next, prev: data.previous});
        });
        setSupportData([]);
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
                                setTopTableData={setTopTableData}
                                getNewData={url => getData(url)}
                                getRelatedData={(url, wrd) =>
                                    getRelatedData(url, wrd)
                                }
                                paginationUrls={paginationUrls}
                            />
                            <Table
                                data={supportData}
                                setTableData={setSupportData}
                                getNewData={url => getData(url)}
                                getRelatedData={(url, wrd) =>
                                    getRelatedData(url, wrd)
                                }
                                paginationUrls={supportPaginationUrls}
                            />
                        </Route>
                    </Switch>
                    <button type="submit" onClick={callFunc}>
                        TestScan
                    </button>
                </div>
            </Router>
        </div>
    );
};
