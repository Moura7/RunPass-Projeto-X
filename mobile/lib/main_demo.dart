import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';

import 'demo_transport.dart';
import 'identity_gateway.dart';
import 'main.dart';

void main() {
  if (!kDebugMode) throw StateError('Demonstration entry point is debug-only');
  final demo = DemoTransport();
  final gateway = IdentityGateway(
    cognito: Uri.parse('https://cognito.demo.invalid'),
    api: Uri.parse('https://api.demo.invalid'),
    clientId: 'demo-not-a-real-client',
    transport: demo.call,
    byteTransport: demo.putBytes,
  );
  runApp(MainApp(gateway: gateway, demonstration: true));
}
