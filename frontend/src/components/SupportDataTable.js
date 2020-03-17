import React from 'react';
import PropTypes from 'prop-types';
import key from 'weak-key';

const SupportDataTable = ({data, mSort}) =>
    !data.length ? (
        <p>Nothing to show</p>
    ) : (
        <div className="column">
            <h2 className="subtitle">
                Showing <strong>{data.length} items</strong>
            </h2>
            <table className="table is-striped">
                <thead>
                    <tr>
                        {Object.entries(data[0]).map(el =>
                            el[0] === 'id' ? (
                                ''
                            ) : (
                                <th onClick={() => mSort(el[0])} key={key(el)}>
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
                                                `http://localhost:8000/api/wordrelation/${el.word}/`
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
        </div>
    );

SupportDataTable.propTypes = {
    data: PropTypes.array.isRequired,
    sortFunc: PropTypes.func
};

export default SupportDataTable;
