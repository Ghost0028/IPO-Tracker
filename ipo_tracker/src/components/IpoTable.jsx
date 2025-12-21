import data from '../data.json'
import './IpoTable.css'

function IpoTable() {
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
              <th>GMP</th>
              <th>Closing Date</th>
              <th>Subscription Rate</th>
            </tr>
          </thead>
          <tbody>
            {data.map((ipo, index) => (
              <tr key={index}>
                <td className="ipo-data">{ipo.ipo}</td>
                <td className="ipo-data">₹{ipo.issuePrice}</td>
                <td className="ipo-data">₹{ipo.gmp}</td>
                <td className='ipo-data'>{ipo.closing}</td>
                <td className="ipo-data">{ipo.subscription}x</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}

export default IpoTable
