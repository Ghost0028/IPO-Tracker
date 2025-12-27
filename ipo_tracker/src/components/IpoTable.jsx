import { useState, useEffect } from 'react';
import './IpoTable.css';

function IpoTable() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filterType,setFilterType]=useState("ALL")
  const [currentPage,setCurrentPage]=useState(1);
  const rowsPerPage=4;

  useEffect(() => {
    fetch('/ipo_react.json')
      .then(res => {
        if (!res.ok) throw new Error('JSON not found');
        return res.json();
      })
      .then(data => {
        setData(data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Load failed:', err);
        setLoading(false);
      });
  }, []);

  
  if (loading) return <div className="ipo-empty-state">🔄 Loading IPOs...</div>;

  const filtered_data= filterType ==="ALL" ? data : data.filter((ipo) => ipo.Type ===filterType) 
  const indexOfLastRow = currentPage * rowsPerPage; 
  const indexOfFirstRow = indexOfLastRow - rowsPerPage; 
  const currentRows = filtered_data.slice(indexOfFirstRow, indexOfLastRow);
  const totalPages = Math.ceil(filtered_data.length / rowsPerPage);

  return (
    <div className='Ipo'>
    <select onChange={(e)=> {
      setFilterType(e.target.value)
      setCurrentPage(1)
      }}>
       <option value="ALL">All Types</option>
       <option value="Main">Main Board</option>
       <option value="SME">SME</option>
    </select>
    
    <div className="ipo-table-container ${currentRows.length === 0 ? 'is-empty' : ''}">
      {currentRows.length === 0 ? (
        <div className="ipo-empty-state">No IPO data available in {filterType} category </div>
      ) : (
        <table className="ipo-table">
          <thead>
            <tr >
              <th>IPO Name</th>
              <th>Issue Price</th>
              <th>Lot Size</th>
              <th>Type</th>
              <th>GMP</th>
              <th>Minimum Capital Required</th>
              <th>Closing Date</th>
              <th>NII</th>
              <th>Retail</th>
              <th>QIB</th>
            </tr>
          </thead>
          <tbody>
            { currentRows.map((ipo) => (
              <tr key={ipo.Name}>
                <td className="ipo-data">{ipo.Name}</td>
                <td className="ipo-data">₹{ipo.Price}</td>
                <td className="ipo-data">{ipo.Lot_size}</td>
                <td className="ipo-data">{ipo.Type}</td>
                <td className="ipo-data">{ipo.GMP}</td>
                <td className="ipo-data">₹{ipo.Minimum_Capital}</td>
                <td className="ipo-data">{ipo.Close_date}</td>
                <td className="ipo-data">{ipo.NII}</td>
                <td className="ipo-data">{ipo.Retail}</td>
                <td className="ipo-data">{ipo.QIB}</td>
              </tr>
            ))}
          </tbody>
        </table>

      )}
      {currentRows.length >0 && (<div className="pagination">
        {Array.from({ length: totalPages }, (_, i) => (
            <button key={i} onClick={() => setCurrentPage(i + 1)}
              className={currentPage === i + 1 ? "active" : ""}
            >
            {i + 1}
            </button>
        ))}
    </div>  
      )}
    </div>
    </div>
  );
}

export default IpoTable;
