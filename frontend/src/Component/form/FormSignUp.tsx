import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import InputField from '../input/InputField';

interface FormData {
    FirstName: string;
    LastName: string;
    email: string;
    password: string;
    birthday: string;
}

const FormSignUp: React.FC = () => {
    const [formData, setFormData] = useState<FormData>({
        FirstName: '',
        LastName: '',
        email: '',
        password: '',
        birthday: ''
    });

    const [error, setError] = useState('');
    const navigate = useNavigate();

    // Fonction pour gérer les changements dans les champs
    const handleChange = (fieldName: keyof FormData, value: string) => {
        setFormData({
            ...formData,
            [fieldName]: value
        });
    };

    // Validation des champs avant la soumission
    const isFormValid = () => {
        if (
            !formData.FirstName ||
            !formData.LastName ||
            !formData.email ||
            !formData.password ||
            !formData.birthday
        ) {
            setError('All fields are required!');
            return false;
        }
        setError('');
        return true;
    };

    // Soumission du formulaire
    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (isFormValid()) {
            console.log("Form Data:", formData);
            navigate('/SignIn'); // Redirection après soumission
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <InputField
                label="First Name"
                type="text"
                name="FirstName"
                value={formData.FirstName}
                onChange={(value) => handleChange('FirstName', value)}
            />
            <InputField
                label="Last Name"
                type="text"
                name="LastName"
                value={formData.LastName}
                onChange={(value) => handleChange('LastName', value)}
            />
            <InputField
                label="Email"
                type="email"
                name="email"
                value={formData.email}
                onChange={(value) => handleChange('email', value)}
            />
            <InputField
                label="Password"
                type="password"
                name="password"
                value={formData.password}
                onChange={(value) => handleChange('password', value)}
            />
            <InputField
                label="Birthday"
                type="date"
                name="birthday"
                value={formData.birthday}
                onChange={(value) => handleChange('birthday', value)}
            />
            {error && <p style={{ color: 'red' }}>{error}</p>}
            <button type="submit">Submit</button>
        </form>
    );
};

export default FormSignUp;

