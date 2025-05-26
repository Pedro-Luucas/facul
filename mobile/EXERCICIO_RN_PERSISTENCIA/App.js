import { useState, useEffect } from "react";
import { FlatList, StyleSheet, View, Alert } from "react-native";
import {
  Appbar,
  Button,
  List,
  PaperProvider,
  Switch,
  Text,
  MD3LightTheme as DefaultTheme,
} from "react-native-paper";
import AsyncStorage from '@react-native-async-storage/async-storage';
import * as Location from 'expo-location';
import * as SQLite from 'expo-sqlite';
import myColors from "./assets/colors.json";
import myColorsDark from "./assets/colorsDark.json";

export default function App() {
  const [isSwitchOn, setIsSwitchOn] = useState(false); // variável para controle do darkMode
  const [isLoading, setIsLoading] = useState(false); // variável para controle do loading do button
  const [locations, setLocations] = useState([]); // variável para armazenar as localizações
  const [db, setDb] = useState(null); // variável para armazenar a instância do banco de dados

  // Carrega tema default da lib RN PAPER com customização das cores
  const [theme, setTheme] = useState({
    ...DefaultTheme,
    myOwnProperty: true,
    colors: myColors.colors,
  });

  // Initialize SQLite database
  async function initDatabase() {
    try {
      const database = await SQLite.openDatabaseAsync('locations.db');
      
      // Create locations table if it doesn't exist
      await database.execAsync(`
        CREATE TABLE IF NOT EXISTS locations (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          latitude REAL NOT NULL,
          longitude REAL NOT NULL,
          timestamp TEXT NOT NULL,
          address TEXT
        );
      `);
      
      setDb(database);
      console.log('Database initialized successfully');
    } catch (error) {
      console.error('Error initializing database:', error);
      Alert.alert('Erro', 'Falha ao inicializar o banco de dados');
    }
  }

  // load darkMode from AsyncStorage
  async function loadDarkMode() {
    try {
      const savedDarkMode = await AsyncStorage.getItem('darkMode');
      if (savedDarkMode !== null) {
        const isDarkMode = JSON.parse(savedDarkMode);
        setIsSwitchOn(isDarkMode);
      }
    } catch (error) {
      console.error('Error loading dark mode:', error);
    }
  }

  // save darkMode to AsyncStorage
  async function saveDarkMode(isDark) {
    try {
      await AsyncStorage.setItem('darkMode', JSON.stringify(isDark));
    } catch (error) {
      console.error('Error saving dark mode:', error);
    }
  }

  // darkMode switch event
  async function onToggleSwitch() {
    const newDarkMode = !isSwitchOn;
    setIsSwitchOn(newDarkMode);
    await saveDarkMode(newDarkMode);
  }

  // Request location permissions
  async function requestLocationPermission() {
    try {
      const { status } = await Location.requestForegroundPermissionsAsync();
      
      if (status !== 'granted') {
        Alert.alert(
          'Permissão Negada',
          'É necessário permitir o acesso à localização para usar esta funcionalidade.'
        );
        return false;
      }
      
      return true;
    } catch (error) {
      console.error('Error requesting location permission:', error);
      Alert.alert('Erro', 'Falha ao solicitar permissão de localização');
      return false;
    }
  }

  // get location (botão capturar localização)
  async function getLocation() {
    if (!db) {
      Alert.alert('Erro', 'Banco de dados não inicializado');
      return;
    }

    setIsLoading(true);

    try {
      // Request permission first
      const hasPermission = await requestLocationPermission();
      if (!hasPermission) {
        setIsLoading(false);
        return;
      }

      // Get current location
      const location = await Location.getCurrentPositionAsync({
        accuracy: Location.Accuracy.High,
      });

      const { latitude, longitude } = location.coords;
      const timestamp = new Date().toISOString();

      // Optionally get address from coordinates
      let address = '';
      try {
        const reverseGeocode = await Location.reverseGeocodeAsync({
          latitude,
          longitude,
        });
        
        if (reverseGeocode.length > 0) {
          const location = reverseGeocode[0];
          address = `${location.street || ''} ${location.streetNumber || ''}, ${location.city || ''}, ${location.region || ''}`.trim();
        }
      } catch (geocodeError) {
        console.log('Geocoding failed:', geocodeError);
        // Continue without address if geocoding fails
      }

      // Save to database
      await saveLocationToDb(latitude, longitude, timestamp, address);
      
      // Reload locations from database
      await loadLocations();

      Alert.alert('Sucesso', 'Localização capturada e salva com sucesso!');

    } catch (error) {
      console.error('Error getting location:', error);
      Alert.alert('Erro', 'Falha ao capturar localização. Verifique se o GPS está ativo.');
    } finally {
      setIsLoading(false);
    }
  }

  // Save location to SQLite database
  async function saveLocationToDb(latitude, longitude, timestamp, address = '') {
    try {
      await db.runAsync(
        'INSERT INTO locations (latitude, longitude, timestamp, address) VALUES (?, ?, ?, ?)',
        [latitude, longitude, timestamp, address]
      );
      console.log('Location saved to database');
    } catch (error) {
      console.error('Error saving location:', error);
      throw error;
    }
  }

  // load locations from db sqlite
  async function loadLocations() {
    if (!db) {
      console.log('Database not initialized yet');
      return;
    }

    setIsLoading(true);

    try {
      const result = await db.getAllAsync('SELECT * FROM locations ORDER BY id DESC');
      setLocations(result);
      console.log(`Loaded ${result.length} locations from database`);
    } catch (error) {
      console.error('Error loading locations:', error);
      Alert.alert('Erro', 'Falha ao carregar localizações do banco de dados');
    } finally {
      setIsLoading(false);
    }
  }

  // Delete location from database (optional feature)
  async function deleteLocation(locationId) {
    try {
      await db.runAsync('DELETE FROM locations WHERE id = ?', [locationId]);
      await loadLocations(); // Reload the list
      Alert.alert('Sucesso', 'Localização removida com sucesso!');
    } catch (error) {
      console.error('Error deleting location:', error);
      Alert.alert('Erro', 'Falha ao remover localização');
    }
  }

  // Format timestamp for display
  function formatTimestamp(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleDateString('pt-BR') + ' ' + date.toLocaleTimeString('pt-BR');
  }

  // Use Effect para inicializar o banco, carregar o darkMode e as localizações
  useEffect(() => {
    async function initializeApp() {
      await initDatabase();
      await loadDarkMode();
    }
    
    initializeApp();
  }, []);

  // Load locations when database is ready
  useEffect(() => {
    if (db) {
      loadLocations();
    }
  }, [db]);

  // Efetiva a alteração do tema dark/light quando a variável isSwitchOn é alterada
  useEffect(() => {
    if (isSwitchOn) {
      setTheme({ ...theme, colors: myColorsDark.colors });
    } else {
      setTheme({ ...theme, colors: myColors.colors });
    }
  }, [isSwitchOn]);

  return (
    <PaperProvider theme={theme}>
      <Appbar.Header>
        <Appbar.Content title="My Location BASE" />
      </Appbar.Header>
      <View style={{ backgroundColor: theme.colors.background, flex: 1 }}>
        <View style={styles.containerDarkMode}>
          <Text>Dark Mode</Text>
          <Switch value={isSwitchOn} onValueChange={onToggleSwitch} />
        </View>
        
        <Button
          style={styles.containerButton}
          icon="map"
          mode="contained"
          loading={isLoading}
          onPress={getLocation}
        >
          Capturar localização
        </Button>

        <View style={styles.locationCount}>
          <Text style={{ color: theme.colors.onBackground }}>
            Total de localizações: {locations.length}
          </Text>
        </View>

        <FlatList
          style={styles.containerList}
          data={locations}
          keyExtractor={(item) => item.id.toString()}
          renderItem={({ item }) => (
            <List.Item
              title={`Localização ${item.id}`}
              description={`Lat: ${item.latitude.toFixed(6)} | Lng: ${item.longitude.toFixed(6)}\n${formatTimestamp(item.timestamp)}${item.address ? `\n${item.address}` : ''}`}
              left={(props) => <List.Icon {...props} icon="map-marker" />}
              right={(props) => (
                <Button
                  {...props}
                  icon="delete"
                  mode="text"
                  compact
                  onPress={() => {
                    Alert.alert(
                      'Confirmar',
                      'Deseja remover esta localização?',
                      [
                        { text: 'Cancelar', style: 'cancel' },
                        { text: 'Remover', onPress: () => deleteLocation(item.id) }
                      ]
                    );
                  }}
                />
              )}
            />
          )}
          ListEmptyComponent={
            <View style={styles.emptyList}>
              <Text style={{ color: theme.colors.onBackground, textAlign: 'center' }}>
                Nenhuma localização salva ainda.{'\n'}
                Toque em "Capturar localização" para começar.
              </Text>
            </View>
          }
        />
      </View>
    </PaperProvider>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
    alignItems: "center",
    justifyContent: "center",
  },
  containerDarkMode: {
    margin: 10,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
  },
  containerButton: {
    margin: 10,
  },
  locationCount: {
    marginHorizontal: 10,
    marginBottom: 10,
  },
  containerList: {
    margin: 10,
    flex: 1,
  },
  emptyList: {
    padding: 20,
    alignItems: 'center',
    justifyContent: 'center',
  },
});