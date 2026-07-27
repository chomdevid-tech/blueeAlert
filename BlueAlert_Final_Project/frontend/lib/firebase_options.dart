

import 'package:firebase_core/firebase_core.dart' show FirebaseOptions;
import 'package:flutter/foundation.dart' show kIsWeb;

class DefaultFirebaseOptions {
  static FirebaseOptions get currentPlatform {
    if (kIsWeb) {
      return web;
    }

    throw UnsupportedError('BlueAlert Firebase is configured for Web only.');
  }

  static const FirebaseOptions web = FirebaseOptions(
    apiKey: 'AIzaSyBXFx37ortnkpWKtKGpdKkkXoBgAek6aww',
    appId: '1:804056850566:web:485124a111fcc793e17107',
    messagingSenderId: '804056850566',
    projectId: 'bluealert-cee60',
    authDomain: 'bluealert-cee60.firebaseapp.com',
    databaseURL:
        'https://bluealert-cee60-default-rtdb.asia-southeast1.firebasedatabase.app',
    storageBucket: 'bluealert-cee60.firebasestorage.app',
    measurementId: 'G-R4JDPN2MQB',
  );
}
