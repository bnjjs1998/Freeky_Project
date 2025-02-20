import React, { useState } from 'react';

// Définition de l'interface Event
interface Event {
    name: string;
    description: string;
    date: string;
    location: string;
    invitesNumber: number;  // 🔹 Correction : camelCase pour matcher le backend
}

const FormEvent: React.FC = () => {
    const [eventData, setEventData] = useState<Event>({
        name: '',
        description: '',
        date: '',
        location: '',
        invitesNumber: 0,
    });

    // Gestion des changements de champs
    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setEventData((prevState) => ({
            ...prevState,
            [name]: name === 'invitesNumber' ? parseInt(value, 10) : value, // Conversion en entier pour invitesNumber
        }));
    };

    // Soumettre les données et afficher en console
    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        console.log("Données de l'événement à envoyer via GraphQL :", eventData);

        // Mutation GraphQL pour créer un événement
        const query = `
        mutation {
            createEvent(
                name: "${eventData.name}",
                description: "${eventData.description}",
                date: "${eventData.date}",
                location: "${eventData.location}",
                invitesNumber: ${eventData.invitesNumber}
            ) {
                success
                event {
                    name
                    description
                    date
                    location
                    invitesNumber
                }
            }
        }
    `;
        
        // Requête fetch pour envoyer la mutation GraphQL
        try {
            const response = await fetch('http://localhost:5001/graphql', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query }),
            });

            const result = await response.json();

            if (result.errors) {
                console.error("Erreur GraphQL :", result.errors);
                return;
            }

            console.log("Réponse GraphQL :", result.event);
            alert("Événement créé avec succès !");
        } catch (error) {
            console.error("Erreur lors de la requête :", error);
            alert("Une erreur est survenue lors de la création de l'événement.");
        }
    };

    return (
        <div>
            {/* <h2> create event</h2> */}
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Event title :</label>
                    <input
                        type="text"
                        name="name"
                        value={eventData.name}
                        onChange={handleInputChange}
                    />
                </div>

                <div>
                    <label>Description :</label>
                    <input
                        type="text"
                        name="description"
                        value={eventData.description}
                        onChange={handleInputChange}
                    />
                </div>

                <div>
                    <label>Date :</label>
                    <input
                        type="date"
                        name="date"
                        value={eventData.date}
                        onChange={handleInputChange}
                    />
                </div>

                <div>
                    <label>Location :</label>
                    <input
                        type="text"
                        name="location"
                        value={eventData.location}
                        onChange={handleInputChange}
                    />
                </div>

                <div>
                    <label>guest number :</label>
                    <input
                        type="number"
                        name="invitesNumber"
                        value={eventData.invitesNumber}
                        onChange={handleInputChange}
                    />
                </div>

                <button type="submit">create my event</button>
            </form>
        </div>
    );
};

export default FormEvent;

