
import './App.scss'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import SignUp from './views/SignUp/SignUp.tsx'
import SignIn from './views/SignIn/SignIn.tsx'
import Profil from './views/Profil/Profil.tsx'

function App() {


  return (
    <>

      <Routes>
        <Route path='/' element={<SignIn />} />
        <Route path='/SignIn' element={<SignUp />} />
        <Route path='/SignUp' element={<SignUp />} />
        <Route path='/Profil' element={<Profil />} />
      </Routes>

    </>
  )
}

export default App
