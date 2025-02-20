import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ApolloProvider } from '@apollo/client';
import client from './services/ApolloClient';
import SignUp from './views/SignUp/SignUp';
import SignIn from './views/SignIn/SignIn';
import Profil from './views/Profil/Profil';
import EventsList from './Component/eventsList/EventsList';

function App() {
  return (
    <ApolloProvider client={client}>
      <Router> {/* 🔹 Ajout du Router ici */}
        <Routes>
          <Route path='/' element={<SignIn />} />
          <Route path='/SignIn' element={<SignIn />} />
          <Route path='/SignUp' element={<SignUp />} />
          <Route path='/Profil' element={<Profil />} />
          <Route path='/Events' element={<EventsList />} />
        </Routes>
      </Router>
    </ApolloProvider>
  );
}

export default App;
