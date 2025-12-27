import './App.css'
import IpoTable from './components/IpoTable'

function App() {
 
  return (
    <div className="App">
      <header className="page-header">
        <h1>IPO Tracker</h1>
        <p>Stay updated with the latest open IPOs</p>
      </header>

      <IpoTable />

      <footer className="page-footer">
        <p>Data auto-refreshed twice daily • Powered by React</p>
      </footer>
    </div>
  )
}

export default App
