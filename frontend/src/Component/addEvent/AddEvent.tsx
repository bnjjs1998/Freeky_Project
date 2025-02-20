import React, { useState } from "react";
import { useMutation } from "@apollo/client";
import { CREATE_EVENT } from "../../services/Mutations";

const AddEvent = () => {
  const [name, setName] = useState("");
  const [date, setDate] = useState("");
  const [location, setLocation] = useState("");
  const [guestsList, setGuestsList] = useState("");
  const [invitesNumber, setInvitesNumber] = useState(0);

  const [createEvent, { data, loading, error }] = useMutation(CREATE_EVENT);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await createEvent({
        variables: {
          name,
          date,
          location,
          guestsList: guestsList.split(","), // Convertir en liste
          invitesNumber: parseInt(invitesNumber.toString(), 10), // 10 est la base décimale
        },
      });
      alert("Événement ajouté !");
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div>
      <h2>Ajouter un Événement</h2>
      <form onSubmit={handleSubmit}>
        <input type="text" placeholder="Nom" value={name} onChange={(e) => setName(e.target.value)} required />
        <input type="date" placeholder="Date" value={date} onChange={(e) => setDate(e.target.value)} required />
        <input type="text" placeholder="Lieu" value={location} onChange={(e) => setLocation(e.target.value)} required />
        <input type="text" placeholder="Invités (séparés par une virgule)" value={guestsList} onChange={(e) => setGuestsList(e.target.value)} />
        <input type="number" placeholder="Nombre d'invitations" value={invitesNumber} onChange={(e) => setInvitesNumber(Number(e.target.value))} required />
        <button type="submit" disabled={loading}>
          {loading ? "Ajout en cours..." : "Ajouter"}
        </button>
      </form>
      {error && <p style={{ color: "red" }}>Erreur: {error.message}</p>}
      {data && <p style={{ color: "green" }}>Événement ajouté avec succès !</p>}
    </div>
  );
};

export default AddEvent;
