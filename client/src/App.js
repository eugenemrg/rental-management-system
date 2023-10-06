import {Route, Routes} from 'react-router-dom'
import { RequireAuth } from 'react-auth-kit'
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
        <Route path='dashboard' element={ 
          <RequireAuth loginPath='/login'>
            <Home/>
          </RequireAuth>
         } />
        <Route path='properties' element={ 
          <RequireAuth loginPath='/login'>
            <Properties/>
          </RequireAuth>
         } />
        <Route path='houses' element={ 
          <RequireAuth loginPath='/login'>
            <Houses/>
          </RequireAuth>
         } />
        <Route path='issues' element={ 
          <RequireAuth loginPath='/login'>
            <Reports/>
          </RequireAuth>
         } />
        <Route path='tenants' element={ 
          <RequireAuth loginPath='/login'>
            <Tenants/>
          </RequireAuth>
         } />
      </Routes>
    </div>
  );
}

export default App;
