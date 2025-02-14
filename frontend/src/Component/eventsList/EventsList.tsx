import React from "react";
import { useQuery } from "@apollo/client";
import { GET_ALL_EVENTS } from "../../services/Queries";

const EventList: React.FC = () => {
  const { loading, error, data } = useQuery(GET_ALL_EVENTS);

  if (loading) return <p>Chargement...</p>;
  if (error) return <p>Erreur: {error.message}</p>;
  if (!data || !data.allEvents) return <p>Aucune donnée reçue.</p>;


  return (
    <div>
      <h2>Liste des Événements</h2>
      {data.allEvents.length === 0 ? (
        <p>Aucun événement disponible.</p>
      ) : (
      <ul>
        {data.allEvents.map((event: 
          { id: string; 
            name: string; 
            description: string; 
            date: string; location: 
            string; invitesNumber: 
            number; guestsList: 
            string[] 
          }) => (
          <li key={event.id}>
            <h3>{event.name}</h3>
            <p>{event.description}</p>
            <p><strong>Date:</strong> {event.date}</p>
            <p><strong>Lieu:</strong> {event.location}</p>
            <p><strong>Nombre d'invitations disponible:</strong> {event.invitesNumber}</p>
            <p><strong>Invités:</strong> {event.guestsList.length > 0 ? event.guestsList.join(", ") : "Aucun invité"}</p>
          </li>
        ))}
      </ul>
    )}
  </div>
)};

export default EventList;
