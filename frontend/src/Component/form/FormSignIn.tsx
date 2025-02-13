import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import InputField from '../input/InputField';
import './FormSignIn.scss'

interface SignInData {
    email: string;
    password: string;
}

const FormSignIn: React.FC = () => {
    const [signInData, setSignInData] = useState<SignInData>({
        email: '',
        password: ''
    });

    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleChange = (fieldName: keyof SignInData, value: string) => {
        setSignInData({
            ...signInData,
            [fieldName]: value
        });
    };

    const isFormValid = () => {
        if (!signInData.email || !signInData.password) {
            setError('Both email and password are required!');
            return false;
        }
        setError('');
        return true;
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (isFormValid()) {
            try {
                await login();
                navigate('/Profil'); // Redirige l'utilisateur vers le tableau de bord
            } catch (error) {
                console.error("Erreur lors de la connexion:", error);
            }
        }
    };

    const login = async () => {
        const query = `
            mutation {
                login(
                    email: "${signInData.email}",
                    password: "${signInData.password}"
                ) {
                    token
                    user {
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
                alert("Échec de la connexion: " + result.errors[0].message);
                return;
            }

            console.log("Réponse GraphQL:", result);

            if (result.data.login.token) {
                alert("Connexion réussie !");
                // Stocker le token si nécessaire
                localStorage.setItem('authToken', result.data.login.token);
            }
        } catch (error) {
            console.error("Erreur lors de la requête:", error);
            alert("Une erreur est survenue lors de la connexion.");
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <InputField
                label="Email"
                type="email"
                name="email"
                value={signInData.email}
                onChange={(value) => handleChange('email', value)}
            />
            <InputField
                label="Password"
                type="password"
                name="password"
                value={signInData.password}
                onChange={(value) => handleChange('password', value)}
            />
            {error && <p style={{ color: 'red' }}>{error}</p>}
            <button type="submit">Sign In</button>
        </form>
    );
};

export default FormSignIn;
