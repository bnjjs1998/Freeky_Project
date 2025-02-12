import React from 'react'
import FormSignIn from '../../Component/form/FormSignIn'
import { Link } from 'react-router-dom'



function SignIn({ }: any) {
    return (
        <>
            <h1>Sign In</h1>
            <FormSignIn />
            <Link to={'/SignUp'}><h2> do you already have account ? sign Up</h2></Link>
        </>
    )
}

export default SignIn