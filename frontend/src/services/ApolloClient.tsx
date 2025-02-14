import { ApolloClient, InMemoryCache } from "@apollo/client";

const client = new ApolloClient({
  uri: "http://localhost:5001/graphql",  // Assure-toi que l'URL est correcte
  cache: new InMemoryCache(),
});

export default client;
