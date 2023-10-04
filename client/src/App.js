import {Route, Routes} from 'react-router-dom'
import './App.css';
import Landing from './components/Landing'
import LogIn_SignUp from './components/LogIn_SignUP'
import Home from './components/Home'
import Properties from './components/Properties'
import Houses from './components/Houses'
import Tenants from './components/Tenants'
import Reports from './components/Reports'

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path='/' element={ <Landing/> } />
        <Route path='login' element={ <LogIn_SignUp/> } />
        <Route path='dashboard' element={ <Home/> } />
        <Route path='properties' element={ <Properties/> } />
        <Route path='houses' element={ <Houses/> } />
        <Route path='issues' element={ <Reports/> } />
        <Route path='tenants' element={ <Tenants/> } />
      </Routes>
    </div>
  );
}

export default App;
