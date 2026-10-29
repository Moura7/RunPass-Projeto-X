import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:runpass/demo_transport.dart';
import 'package:runpass/catalog_screen.dart';
import 'package:runpass/identity_gateway.dart';
import 'package:runpass/main.dart';

IdentityGateway demoGateway(DemoTransport demo) => IdentityGateway(
  cognito: Uri.parse('https://cognito.demo.invalid'),
  api: Uri.parse('https://api.demo.invalid'),
  clientId: 'synthetic-client',
  transport: demo.call,
);

void main() {
  testWidgets(
    'clearly labelled local demo goes from login through profile and admission to catalog',
    (tester) async {
      final gateway = demoGateway(DemoTransport());
      await tester.pumpWidget(MainApp(gateway: gateway, demonstration: true));
      expect(find.textContaining('DEMONSTRAÇÃO LOCAL'), findsOneWidget);
      await tester.enterText(
        find.widgetWithText(TextFormField, 'E-mail'),
        'demo@runpass.test',
      );
      await tester.enterText(
        find.widgetWithText(TextFormField, 'Senha'),
        'RunpassDemo123!',
      );
      await tester.ensureVisible(find.text('Continuar'));
      await tester.tap(find.text('Continuar'));
      await tester.pumpAndSettle();
      await tester.enterText(
        find.widgetWithText(TextFormField, 'Nome de exibição'),
        'Corredor Demo',
      );
      await tester.enterText(
        find.widgetWithText(TextFormField, 'Nome de usuário'),
        'corredor_demo',
      );
      await tester.ensureVisible(find.text('Continuar'));
      await tester.tap(find.text('Continuar'));
      await tester.pumpAndSettle();
      await tester.enterText(
        find.widgetWithText(TextFormField, 'Data de nascimento (AAAA-MM-DD)'),
        '1990-01-01',
      );
      await tester.ensureVisible(find.byType(CheckboxListTile));
      await tester.tap(find.byType(CheckboxListTile));
      await tester.pumpAndSettle();
      await tester.ensureVisible(find.text('Continuar'));
      await tester.tap(find.text('Continuar'));
      await tester.pumpAndSettle();
      await tester.ensureVisible(find.text('Explorar corridas'));
      await tester.tap(find.text('Explorar corridas'));
      await tester.pumpAndSettle();
      expect(find.text('Descobrir corridas'), findsOneWidget);
      await tester.scrollUntilVisible(
        find.text('Carregar mais').hitTestable(),
        400,
        scrollable: find
            .descendant(
              of: find.byType(CatalogScreen),
              matching: find.byType(Scrollable),
            )
            .first,
      );
      expect(find.text('Carregar mais'), findsOneWidget);
    },
  );

  test(
    'demo signup and confirmation never contact a network service',
    () async {
      final gateway = demoGateway(DemoTransport());
      await gateway.signUp('new@runpass.test', 'RunpassDemo123!');
      await gateway.confirm('new@runpass.test', '123456');
      await gateway.signIn('new@runpass.test', 'RunpassDemo123!');
      expect(
        (await gateway.request('/beta/status'))['myStatus'],
        'not_admitted',
      );
      await gateway.forgot('new@runpass.test');
      await gateway.reset('new@runpass.test', '123456', 'RunpassChanged123!');
      await gateway.signOut();
      expect(gateway.signedIn, false);
      await gateway.signIn('new@runpass.test', 'RunpassChanged123!');
      expect(gateway.signedIn, true);
    },
  );
}
