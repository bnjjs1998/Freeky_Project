import React from 'react'
import FormEvent from '../../Component/form/FormEvent'
import { useNavigate } from 'react-router-dom'


function Profil({ }: any) {
    const navigate = useNavigate()
    const handleRedirect = () => {
        navigate('/Events')
    }
    return (
        <>
            <button onClick={handleRedirect}>Back</button>
            <div>

            <h1>Create your event</h1>
            <FormEvent />
            </div>
        </>
    )
}

export default Profil