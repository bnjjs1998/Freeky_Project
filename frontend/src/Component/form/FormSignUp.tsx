import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import InputField from '../input/InputField';

interface FormData {
    FirstName: string;
    LastName: string;
    email: string;
    password: string;
    birthdate: string;
}

const FormSignUp: React.FC = () => {
    const [formData, setFormData] = useState<FormData>({
        FirstName: '',
        LastName: '',
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
            !formData.FirstName ||
            !formData.LastName ||
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
        const formattedBirthday = new Date(formData.birthdate).toISOString().split("T")[0];

        const query = `
            mutation {
                register(
                    FirstName: "${formData.FirstName}",
                    LastName: "${formData.LastName}",
                    birthdate: "${formattedBirthday}",
                    email: "${formData.email}",
                    password: "${formData.password}"
                ) {
                    user {
                        FirstName
                        LastName
                        birthdate
                        email
                    }
                }
            }
        `;

        try {
            const response = await fetch("http://localhost:5000/graphql", {
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

            if (result.data.register.user) {
                alert("Utilisateur créé avec succès !");
            }
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
