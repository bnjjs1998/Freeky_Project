import React from "react";
import { useQuery } from "@apollo/client";
import { GET_ALL_EVENTS } from "../../services/Queries";
import { useNavigate } from "react-router-dom";
import "./EventList.scss"

const EventList: React.FC = () => {
  const { loading, error, data } = useQuery(GET_ALL_EVENTS);

  const navigate = useNavigate();
  const handleRedirect = () => {
    navigate('/Profil')
}

  if (loading) return <p>Chargement...</p>;
  if (error) return <p>Erreur: {error.message}</p>;
  if (!data || !data.allEvents) return <p>Aucune donnée reçue.</p>;


  return (
  <div className="wrapper" style={{display:'flex', width:'100vw', justifyContent: 'center', gap: '1rem'}}>
    <div className="content" style={{display:'flex', flexDirection: 'column', gap: '2rem'}}>
      <h1>Liste des Événements</h1>
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
          <li key={event.id} style={{ margin: '1rem 0'}}>
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
    <button onClick={handleRedirect}>Add New Event</button>
    </div>
  </div>
 
)};

export default EventList;
