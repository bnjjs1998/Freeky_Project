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

            <h1>All Events list</h1>
            {/* <h6>create event</h6> */}
            <FormEvent />
            </div>
        </>
    )
}

export default Profil