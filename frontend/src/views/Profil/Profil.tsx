import './Profil.scss'
import FormEvent from '../../Component/form/FormEvent'
import { useNavigate } from 'react-router-dom'


function Profil({ }: any) {
    const navigate = useNavigate()
    const handleRedirect = () => {
        navigate('/Events')
    }
    return (
        <>
            <div className='wrapper'>
            <button onClick={handleRedirect}>Back</button>

            <h1>Create your event</h1>
            <FormEvent />
            </div>
        </>
    )
}

export default Profil