import './App.css'
import IpoTable from './components/IpoTable'
import Navbar from './components/Navbar'

function App() {
 
  return (
    <div className="App">
      <Navbar />
      <header className="page-header">
        <h2>IPO Tracker</h2>
        <p>Stay updated with the latest open IPOs</p>
      </header>

      <IpoTable />

      <footer className="page-footer">
        <p>Data auto-refreshed every 6 hours • Powered by React</p>
        <p className="page-footer">
        Disclaimer: GMP does not represent the actual listing price. It can vary based on demand. 
        We are not promoting any IPOs. Please do your own analysis before investing.
        </p>
      </footer>
    </div>
  )
}

export default App
