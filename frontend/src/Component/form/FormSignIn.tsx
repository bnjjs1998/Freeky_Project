import React from 'react'
import InputField from '../input/InputField';


function FormSignIn({ }: any) {

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
    };


    return (
        <>
            <form onSubmit={handleSubmit}>

            </form>
        </>
    )
}


export default FormSignIn