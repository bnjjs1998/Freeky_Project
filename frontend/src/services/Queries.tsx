import { gql } from "@apollo/client";

export const GET_ALL_EVENTS = gql`
  query GetAllEvents {
    allEvents {
      id
      name
      description
      date
      location
      invitesNumber
      guestsList
    }
  }
`;
