import { gql } from "@apollo/client";

export const CREATE_EVENT = gql`
  mutation CreateEvent(
    $name: String!
    $date: String!
    $location: String!
    $invitesNumber: Int!
  ) {
    createEvent(
      name: $name
      date: $date
      location: $location
      invitesNumber: $invitesNumber
    ) {
      success
      event {
        name
        date
        location
        invitesNumber
      }
    }
  }
`;
