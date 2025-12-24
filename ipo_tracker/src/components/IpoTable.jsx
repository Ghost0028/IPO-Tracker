import { useState, useEffect } from 'react';
import './IpoTable.css';

function IpoTable() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

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

  return (
    <div className="ipo-table-container">
      {data.length === 0 ? (
        <div className="ipo-empty-state">No IPO data available</div>
      ) : (
        <table className="ipo-table">
          <thead>
            <tr>
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
            {data.map((ipo) => (
              <tr >
                <td className="ipo-data">{ipo.Name}</td>
                <td className="ipo-data">₹{ipo.Price}</td>
                <td className="ipo-data">₹{ipo.Lot_size}</td>
                <td className="ipo-data">₹{ipo.Type}</td>
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
    </div>
  );
}

export default IpoTable;
