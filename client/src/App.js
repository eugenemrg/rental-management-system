import {Route, Routes} from 'react-router-dom'
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import Landing from './components/Landing'
import Login from './components/Login'; 
import SignUp from './components/SignUp';
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
        <Route path='login' element={<Login />} />
        <Route path='signup' element={<SignUp />} />
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
