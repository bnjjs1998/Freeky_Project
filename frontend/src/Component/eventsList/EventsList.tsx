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
            cover: string;
            date: string;
            location: string;
            invitesNumber: number;
            guestsList: string[] 
          }) => (
            <li key={event.id} style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gridTemplateRows: "auto auto", gap: "1rem", margin: '1rem 0', border: "solid 2px #ff3366", borderRadius: "12px", padding: '.5rem', backgroundColor: "#1b1b1b" }}>
              <h3 style={{ gridColumn: "1 / span 2", fontSize: "1.5rem" }}>{event.name}</h3>
              <div className="left" style={{ gridColumn: "1 / 2" }}>
                <img src={event.cover} alt="event cover" />
              </div>
              <div className="right" style={{ gridColumn: "2 / 3" }}>
                <p>{event.description}</p>
                <p><strong>Date:</strong> {event.date}</p>
                <p><strong>Lieu:</strong> {event.location}</p>
                <p><strong>Nombre de place disponible:</strong> {event.invitesNumber}</p>
              {/* <p><strong>Invités:</strong> {event.guestsList.length > 0 ? event.guestsList.join(", ") : "Aucun participant à ce jour"}</p> */}
              </div>
            </li>
        ))}
      </ul>
    )}
    <button onClick={handleRedirect}>Add New Event</button>
    </div>
  </div>
 
)};

export default EventList;
