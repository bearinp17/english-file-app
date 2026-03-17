/**
 * English File Mobile App
 * React Native application for language learning
 */

import React, { useState, useEffect } from 'react';
import { 
  StyleSheet, 
  Text, 
  View, 
  TouchableOpacity, 
  ScrollView,
  FlatList,
  SafeAreaView
} from 'react-native';

// API Configuration
const API_URL = 'http://localhost:8000';

// ==================== COMPONENTS ====================

// Level Card Component
const LevelCard = ({ level, onPress }) => (
  <TouchableOpacity style={styles.levelCard} onPress={onPress}>
    <Text style={styles.levelNumber}>Level {level.id}</Text>
    <Text style={styles.levelName}>{level.name}</Text>
    <Text style={styles.levelCefr}>{level.cefr}</Text>
    <Text style={styles.levelDesc}>{level.description}</Text>
  </TouchableOpacity>
);

// Lesson Card Component
const LessonCard = ({ lesson, onPress }) => (
  <TouchableOpacity style={styles.lessonCard} onPress={onPress}>
    <Text style={styles.lessonTitle}>{lesson.title}</Text>
    <Text style={styles.lessonPreview}>
      {lesson.content.substring(0, 100)}...
    </Text>
  </TouchableOpacity>
);

// ==================== SCREENS ====================

// Home Screen
const HomeScreen = ({ navigation }) => {
  const [levels, setLevels] = useState([]);

  useEffect(() => {
    // Fetch levels from API
    fetch(`${API_URL}/levels`)
      .then(res => res.json())
      .then(data => setLevels(data))
      .catch(err => console.log(err));
  }, []);

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>English File</Text>
        <Text style={styles.headerSubtitle}>Learn English step by step</Text>
      </View>
      <FlatList
        data={levels}
        keyExtractor={item => item.id.toString()}
        renderItem={({ item }) => (
          <LevelCard 
            level={item} 
            onPress={() => navigation.navigate('Lessons', { levelId: item.id })}
          />
        )}
        contentContainerStyle={styles.list}
      />
    </SafeAreaView>
  );
};

// Lessons Screen
const LessonsScreen = ({ route, navigation }) => {
  const { levelId } = route.params;
  const [lessons, setLessons] = useState([]);

  useEffect(() => {
    fetch(`${API_URL}/levels/${levelId}/lessons`)
      .then(res => res.json())
      .then(data => setLessons(data))
      .catch(err => console.log(err));
  }, [levelId]);

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Level {levelId}</Text>
        <TouchableOpacity onPress={() => navigation.goBack()}>
          <Text style={styles.backButton}>← Back</Text>
        </TouchableOpacity>
      </View>
      <FlatList
        data={lessons}
        keyExtractor={item => item.id}
        renderItem={({ item }) => (
          <LessonCard 
            lesson={item} 
            onPress={() => navigation.navigate('Lesson', { lessonId: item.id })}
          />
        )}
        contentContainerStyle={styles.list}
      />
    </SafeAreaView>
  );
};

// Lesson Detail Screen
const LessonDetailScreen = ({ route, navigation }) => {
  const { lessonId } = route.params;
  const [lesson, setLesson] = useState(null);

  useEffect(() => {
    fetch(`${API_URL}/lessons/${lessonId}`)
      .then(res => res.json())
      .then(data => setLesson(data))
      .catch(err => console.log(err));
  }, [lessonId]);

  if (!lesson) return <View><Text>Loading...</Text></View>;

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView>
        <View style={styles.header}>
          <TouchableOpacity onPress={() => navigation.goBack()}>
            <Text style={styles.backButton}>← Back</Text>
          </TouchableOpacity>
          <Text style={styles.headerTitle}>{lesson.title}</Text>
        </View>
        <View style={styles.content}>
          <Text style={styles.lessonText}>{lesson.content}</Text>
        </View>
        <TouchableOpacity 
          style={styles.button}
          onPress={() => navigation.navigate('Exercises', { lessonId })}
        >
          <Text style={styles.buttonText}>Start Exercises →</Text>
        </TouchableOpacity>
      </ScrollView>
    </SafeAreaView>
  );
};

// AI Tutor Screen
const AITutorScreen = () => {
  const [message, setMessage] = useState('');
  const [chat, setChat] = useState([]);

  const sendMessage = () => {
    if (!message.trim()) return;
    
    const userMsg = { role: 'user', text: message };
    setChat([...chat, userMsg]);
    
    // Call AI API
    fetch(`${API_URL}/ai/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, user_id: 'demo' })
    })
    .then(res => res.json())
    .then(data => {
      setChat([...chat, userMsg, { role: 'ai', text: data.response }]);
    });
    
    setMessage('');
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>AI Tutor</Text>
      </View>
      <FlatList
        data={chat}
        keyExtractor={(item, i) => i.toString()}
        renderItem={({ item }) => (
          <View style={[
            styles.chatMessage,
            item.role === 'user' ? styles.userMessage : styles.aiMessage
          ]}>
            <Text>{item.text}</Text>
          </View>
        )}
      />
      <View style={styles.inputContainer}>
        <TextInput
          style={styles.input}
          value={message}
          onChangeText={setMessage}
          placeholder="Type your message..."
        />
        <TouchableOpacity style={styles.sendButton} onPress={sendMessage}>
          <Text style={styles.sendButtonText}>Send</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
};

// ==================== STYLES ====================

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    padding: 20,
    backgroundColor: '#4A90E2',
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
  },
  headerSubtitle: {
    fontSize: 14,
    color: '#ddd',
  },
  backButton: {
    fontSize: 16,
    color: '#fff',
    marginBottom: 10,
  },
  list: {
    padding: 16,
  },
  levelCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 20,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  levelNumber: {
    fontSize: 14,
    color: '#888',
  },
  levelName: {
    fontSize: 20,
    fontWeight: 'bold',
    marginVertical: 4,
  },
  levelCefr: {
    fontSize: 16,
    color: '#4A90E2',
    fontWeight: '600',
  },
  levelDesc: {
    fontSize: 14,
    color: '#666',
    marginTop: 8,
  },
  lessonCard: {
    backgroundColor: '#fff',
    borderRadius: 8,
    padding: 16,
    marginBottom: 12,
  },
  lessonTitle: {
    fontSize: 18,
    fontWeight: '600',
  },
  lessonPreview: {
    fontSize: 14,
    color: '#666',
    marginTop: 4,
  },
  content: {
    padding: 20,
  },
  lessonText: {
    fontSize: 16,
    lineHeight: 24,
  },
  button: {
    backgroundColor: '#4A90E2',
    margin: 20,
    padding: 16,
    borderRadius: 8,
    alignItems: 'center',
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  chatMessage: {
    padding: 12,
    margin: 8,
    borderRadius: 12,
    maxWidth: '80%',
  },
  userMessage: {
    backgroundColor: '#4A90E2',
    alignSelf: 'flex-end',
  },
  aiMessage: {
    backgroundColor: '#fff',
    alignSelf: 'flex-start',
  },
  inputContainer: {
    flexDirection: 'row',
    padding: 10,
    backgroundColor: '#fff',
  },
  input: {
    flex: 1,
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
    padding: 10,
  },
  sendButton: {
    backgroundColor: '#4A90E2',
    padding: 12,
    borderRadius: 8,
    marginLeft: 8,
  },
  sendButtonText: {
    color: '#fff',
  },
});

export default App;
