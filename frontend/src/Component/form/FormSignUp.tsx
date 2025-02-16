import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import InputField from '../input/InputField';
import './FormSignUp.scss'

interface FormData {
    firstName: string;
    lastName: string;
    email: string;
    password: string;
    birthdate: string;
}

const FormSignUp: React.FC = () => {
    const [formData, setFormData] = useState<FormData>({
        firstName: '',
        lastName: '',
        email: '',
        password: '',
        birthdate: ''
    });

    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleChange = (fieldName: keyof FormData, value: string) => {
        setFormData({
            ...formData,
            [fieldName]: value
        });
    };

    const isFormValid = () => {
        if (
            !formData.firstName ||
            !formData.lastName ||
            !formData.email ||
            !formData.password ||
            !formData.birthdate
        ) {
            setError('All fields are required!');
            return false;
        }
        setError('');
        return true;
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (isFormValid()) {
            console.log("Form Data:", formData);
            try {
                await fetchData(); // Assurer que la fonction est bien appelée
                navigate('/SignIn');
            } catch (error) {
                console.error("Erreur lors de l'inscription:", error);
            }
        }
    };

    const fetchData = async () => {
        const formattedBirthdate = new Date(formData.birthdate).toISOString().split("T")[0];

        const query = `
            mutation {
                register(
                    firstName: "${formData.firstName}",
                    lastName: "${formData.lastName}",
                    birthdate: "${formattedBirthdate}",
                    email: "${formData.email}",
                    password: "${formData.password}"
                ) {
                    user {
                        firstName
                        lastName
                        birthdate
                        email
                    }
                }
            }
        `;

        try {
            const response = await fetch("http://localhost:5001/graphql", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ query }),
            });

            const result = await response.json();

            if (result.errors) {
                console.error("Erreur GraphQL:", result.errors);
                alert("Échec de l'inscription: " + result.errors[0].message);
                return;
            }

            console.log("Réponse GraphQL:", result);


        } catch (error) {
            console.error("Erreur lors de la requête:", error);
            alert("Une erreur est survenue lors de l'inscription.");
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <InputField
                label="First Name"
                type="text"
                name="firstName"
                value={formData.firstName}
                onChange={(value) => handleChange('firstName', value)}
            />
            <InputField
                label="Last Name"
                type="text"
                name="lastName"
                value={formData.lastName}
                onChange={(value) => handleChange('lastName', value)}
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
                label="birthdate"
                type="date"
                name="birthdate"
                value={formData.birthdate}
                onChange={(value) => handleChange('birthdate', value)}
            />
            {error && <p style={{ color: 'red' }}>{error}</p>}
            <button type="submit">Submit</button>
        </form>
    );
};

export default FormSignUp;
