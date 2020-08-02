import React, {useState} from 'react';
import key from 'weak-key';

const Table = ({
    data,
    setTopTableData,
    getNewData,
    getRelatedData,
    paginationUrls
}) => {
    const [order, setOrder] = useState({});

    const sortFunc = sortKey => {
        const sortOrder = order[sortKey] ? !order[sortKey] : true;
        const newData = data.sort((obj1, obj2) =>
            obj1[sortKey] > obj2[sortKey]
                ? sortOrder
                    ? -1
                    : 1
                : obj1[sortKey] < obj2[sortKey]
                ? sortOrder
                    ? 1
                    : -1
                : 0
        );
        setOrder({...order, [sortKey]: sortOrder});
        setTopTableData([...newData]);
    };

    return !data.length ? (
        <p>Nothing to show</p>
    ) : (
        <div className="column">
            <h2 className="subtitle">
                Showing <strong>{data.length} items</strong>
            </h2>
            <button onClick={() => getNewData(paginationUrls.prev)}>
                Previous
            </button>
            <button onClick={() => getNewData(paginationUrls.next)}>
                Next
            </button>
            <table className="table is-striped">
                <thead>
                    <tr>
                        {Object.entries(data[0]).map(el =>
                            el[0] === 'id' ? (
                                ''
                            ) : (
                                <th
                                    onClick={() => sortFunc(el[0])}
                                    key={key(el)}>
                                    {el[0]}
                                </th>
                            )
                        )}
                    </tr>
                </thead>
                <tbody>
                    {data.map(el => (
                        <tr key={el.id}>
                            {Object.entries(el).map(el =>
                                el[0] === 'id' ? (
                                    ''
                                ) : (
                                    <td
                                        onClick={() =>
                                            getNewData(
                                                `http://localhost:8000/api/word/${el[1]}/`
                                            )
                                        }
                                        key={key(el)}>
                                        {el[1]}
                                    </td>
                                )
                            )}
                            {el.word ? (
                                <td>
                                    <button
                                        onClick={() =>
                                            getRelatedData(
                                                `http://localhost:8000/api/wordrelation/${el.word}/`,
                                                el.word
                                            )
                                        }>
                                        Get Related words!
                                    </button>
                                </td>
                            ) : (
                                ''
                            )}
                        </tr>
                    ))}
                </tbody>
            </table>
            <button onClick={() => getNewData(paginationUrls.prev)}>
                Previous
            </button>
            <button onClick={() => getNewData(paginationUrls.next)}>
                Next
            </button>
        </div>
    );
};

export default Table;
