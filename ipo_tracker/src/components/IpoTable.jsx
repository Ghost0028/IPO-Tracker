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
              <th>Subscription Rate</th>
            </tr>
          </thead>
          <tbody>
            {data.map((ipo, index) => (
              <tr key={index}>
                <td className="ipo-name">{ipo.ipo}</td>
                <td className="ipo-price">₹{ipo.issuePrice}</td>
                <td className="ipo-gmp">₹{ipo.gmp}</td>
                <td className="ipo-subscription">{ipo.subscription}x</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}

export default IpoTable
